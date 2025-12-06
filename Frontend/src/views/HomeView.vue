<script setup lang="ts">
  import { ref, onMounted } from 'vue';

  function authFetch(url: string, options: any = {}) {
    const token = localStorage.getItem('access');

    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    };

    return fetch(url, { ...options, headers });
  }

  interface Transaction {
    id?: number;
    date: string;
    category: string;
    RefNo: string;
    withdrawal: number;
    deposit: number;
    balance: number;
  }

  const categories = [
    { value: 'FD', text: 'Еда' },
    { value: 'TR', text: 'Транспорт' },
    { value: 'SP', text: 'Шоппинг' },
    { value: 'RT', text: 'Аренда' },
    { value: 'SL', text: 'Зарплата' },
    { value: 'MS', text: 'Другое' },
  ];

  const predictions = [
    {value: 'Misc', text: 'MS'}
  ]

  const transactions = ref<Transaction[]>([]);
  const addingTransaction = ref(false);

  const Date = ref('');
  const Category = ref('');
  const RefNo = ref('');
  const Withdrawal = ref(0);
  const Deposit = ref(0);
  const Balance = ref(0);
  const username = ref();

  function inputDate(event: Event) {
    const target = event.target as HTMLInputElement;
    Date.value = target.value;
  }

  function inputCategory(event: Event) {
    const target = event.target as HTMLSelectElement;
    Category.value = target.value;
  }

  function inputRefNo(event: Event) {
    const target = event.target as HTMLInputElement;
    RefNo.value = target.value;
  }

  function inputWithdrawal(event: Event) {
    const target = event.target as HTMLInputElement;
    Withdrawal.value = parseFloat(target.value);
  }
  function inputDeposit(event: Event) {
    const target = event.target as HTMLInputElement;
    Deposit.value = parseFloat(target.value);
  }
  function inputBalance(event: Event) {
    const target = event.target as HTMLInputElement;
    Balance.value = parseFloat(target.value);
  }

  function formatDate(dateStr: string) {
    const [year, month, day] = dateStr.split('-');
    return `${day}.${month}.${year}`;
  }

  function resetInputFields() {
    Date.value = '';
    Category.value = '';
    RefNo.value = '';
    Withdrawal.value = 0;
    Deposit.value = 0;
    Balance.value = 0;
  }

  function createTransaction() {
    console.log(Date.value);
    const newTransaction = {
      date: Date.value,
      category: Category.value,
      RefNo: RefNo.value,
      withdrawal: Withdrawal.value,
      deposit: Deposit.value,
      balance: Balance.value,
    };

    transactions.value.push(newTransaction);
    resetInputFields();
    addingTransaction.value = false;
  }

  async function getCategotyPrediction(){
    Category.value =  await fetch('http://127.0.0.1:8000/api/v1/predict-category/', {
      method: 'POST',
      headers:{
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        'Withdrawal': Withdrawal.value,
        'Deposite': Deposit.value,
        'Balance': Balance.value
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Ошибка сети: ' + response.status);
      }
      return response.json();
    })
    .then(data => {
      console.log('Ответ сервера:', data);
      return predictions.find(cat => cat.value === data.predicted_category)?.text || ' '
    })
    .catch(error => {
      console.error('Ошибка запроса:', error);
      return ' ';
    });
    console.log(Category.value)
  }

  function logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('user');
    location.href = '/login';
  }

  onMounted(async () => {
    const access = localStorage.getItem('access');
    if (!access) {
      location.href = '/login';
      return;
    }

    // 1. Загружаем профиль
    username.value = await authFetch('http://127.0.0.1:8000/auth/profile/')
      .then(res => {
        if (res.status === 401) {
          location.href = '/login';
          return;
        }
        return res.json();
      })
      .then(data => data?.username)
      .catch(() => {
        location.href = '/login';
      });

    // 2. Загружаем транзакции
    transactions.value = await authFetch('http://127.0.0.1:8000/api/v1/transactions/')
      .then(res => {
        if (res.status === 401) {
          location.href = '/login';
          return [];
        }
        return res.json();
      })
      .then(data => {
        return data.map((t: any, i: number) => {
          const id = t.id ?? t.pk ?? t.ID ?? i;
          return { id, ...t };
        });
      })
      .catch(() => []);
  });
</script>

<template>
  <main>
    <div class="header">
      <h1>Ваш помощник по финансам</h1>
      <div style="display: flex; align-items: right;">
        <button @click="logout" class="nice-button" style="height: 50px; margin-top: 10px; border: solid 1px black">Выйти</button>
        <h1 style="padding-right: 10px; padding-top: 10px;">{{ username }}</h1>
      </div>
    </div>
    <div class="content">
      <div class="welcome">
        <h1>История ваших транзакций:</h1>
      </div><br>
      <button class="nice-button" @click="addingTransaction = !addingTransaction">+ Добавить транзакцию</button><br>
      <div v-if="addingTransaction" class="input-transaction">
        <div class="input-block">
          <h2>Дата транзакции</h2><br>
          <input :value="Date" @input="inputDate" type="date" class="date-picker"/>
        </div>
        <div class="input-block">
          <h2>Категория транзакции</h2><br>
          <div>
          <select :value="Category" @input="inputCategory" class="category-select">
            <option value="FD">Еда</option>
            <option value="TR">Транспорт</option>
            <option value="SP">Шоппинг</option>
            <option value="RT">Аренда</option>
            <option value="SL">Зарплата</option>
            <option value="MS">Другое</option>
          </select>
          <button @click="getCategotyPrediction" class="nice-button" id="predict-button">Предсказать</button>
          </div>
        </div>
        <div class="input-block">
          <h2>ID</h2>
          <input :value="RefNo" @input="inputRefNo" type="text" class="id-input">
        </div>
        <div class="input-block">
          <h2>Списание</h2>
          <input :value="Withdrawal" @input="inputWithdrawal" type="text" class="withdrawal-input">
        </div>
        <div class="input-block">
          <h2>Депозит</h2>
          <input :value="Deposit" @input="inputDeposit" type="text" class="deposit-input">
        </div>
        <div class="input-block">
          <h2>Баланс</h2>
          <input :value="Balance" @input="inputBalance" type="text" class="deposit-input">
        </div>
        <button class="create-transaction" @click="createTransaction">Добавить</button>
      </div>
      <div v-for="transaction in transactions" :key="transaction.id" class="transaction-item">
        <div class="transaction-card">
          <div class="input-block">
            <h2>Дата</h2>
            <h2>{{ formatDate(transaction.date) }}</h2><br>
          </div>
          <div class="input-block">
            <h2>Категория</h2>
            <h2>{{ categories.find(cat => cat.value === transaction.category)?.text || transaction.category }}</h2><br>
          </div>
          <div class="input-block">
            <h2>ID</h2>
            <h2>{{ transaction.RefNo }}</h2>
          </div>
          <div class="input-block">
            <h2>Списание</h2>
            <h2>{{ transaction.withdrawal }}</h2>
          </div>
          <div class="input-block">
            <h2>Депозит</h2>
            <h2>{{ transaction.deposit }}</h2>
          </div>
          <div class="last-input-block">
            <h2>Баланс</h2>
            <h2>{{ transaction.balance }}</h2>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
  .header {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    height: 70px;
    border: solid black;
    border-width: 0px 0px 1px 0px;
    background: #8aff84;
    background: linear-gradient(52deg, rgba(138, 255, 132, 1) 0%, rgba(34, 184, 0, 1) 100%);
  }
  .header h1{
    margin: 1%;
    text-align: left;
    margin-left: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: white;
    font-size: 40px;
    -webkit-text-stroke: 2px #000;
    width: 69%;
  }
  .welcome h1{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #222222;
    font-size: 30px;
    -webkit-text-stroke: 0.5px #000;
    margin-left: 20px;
  }
  .nice-button {
    margin-left: 20px;
    background: #8aff84;
    background: linear-gradient(52deg, rgba(138, 255, 132, 1) 0%, rgba(34, 184, 0, 1) 100%);
    border: none;
    color: white;
    padding: 10px 20px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 24px;
    border-radius: 28px;
    cursor: pointer;
    box-shadow: 0 1px #999;
    transition: transform 0.1s ease, box-shadow 0.1s ease;
  }
  .nice-button:active {
    transform: scale(0.95);
    box-shadow: 0 0 #666;
  }
  .input-transaction{
    margin: 20px;
    border: solid rgb(162, 162, 162) 1px;
    height: 150px;
    border-radius: 30px;
    -webkit-box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
    -moz-box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
    box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
    display: flex;
    flex-direction: row;
  }
  .input-block{
    display: flex;
    flex-direction: column;
    padding-left:20px;
    padding-right:20px;
    border: solid #a2a2a2;
    border-width: 0px 1px 0px 0px;
  }
  .input-block h2{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #222222;
    font-size: 24px;
    -webkit-text-stroke: 0.5px #000;
  }
  .last-input-block h2{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #222222;
    font-size: 24px;
    -webkit-text-stroke: 0.5px #000;
  }
  .date-picker{
    width: 200px;
    height: 30px;
    border-radius: 8px;
    border: solid rgb(162, 162, 162) 1px;
    font-size: 16px;
    padding-left: 10px;
  }
  .category-select{
    width: 200px;
    height: 30px;
    border-radius: 8px;
    border: solid rgb(162, 162, 162) 1px;
    font-size: 16px;
    padding-left: 10px;
  }
  #predict-button{
    margin-top: 0px;
    height: 36px;
    width: 120px;
    font-size: 14px;
  }
  .id-input{
    width: 50px;
    height: 30px;
    border-radius: 8px;
    border: solid rgb(162, 162, 162) 1px;
    font-size: 16px;
    padding-left: 10px;
    margin-top: 20px;
  }
  .withdrawal-input{
    width: 100px;
    height: 30px;
    border-radius: 8px;
    border: solid rgb(162, 162, 162) 1px;
    font-size: 16px;
    padding-left: 10px;
    margin-top: 20px;
  }
  .deposit-input{
    width: 100px;
    height: 30px;
    border-radius: 8px;
    border: solid rgb(162, 162, 162) 1px;
    font-size: 16px;
    padding-left: 10px;
    margin-top: 20px;
  }
  .create-transaction{
    background: #8aff84;
    background: linear-gradient(52deg, rgba(138, 255, 132, 1) 0%, rgba(34, 184, 0, 1) 100%);
    width: 108px;
    border: none;
    border-radius: 0 30px 30px 0;
    color: white;
    padding: 10px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 20px;
    cursor: pointer;
    box-shadow: 0 1px #999;
    transition: transform 0.1s ease, box-shadow 0.1s ease;
  }
  .create-transaction:active {
    transform: scale(0.95);
    box-shadow: 0 0 #666;
  }
  .transaction-card {
    border: solid rgb(162, 162, 162) 1px;
    height: 150px;
    border-radius: 30px;
    -webkit-box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
    -moz-box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
    box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
    display: flex;
    flex-direction: row;
    margin: 12px 20px;
    width: fit-content;
  }
  .input-transaction.small {
    height: 120px;
    border-radius: 16px;
    display: flex;
    gap: 8px;
  }
  .last-input-block {
    display: flex;
    flex-direction: column;
    padding-left:20px;
    padding-right:20px;
  }
</style>
