<script setup lang="ts">
import { ref } from 'vue';

const name = ref('');
const email = ref('');
const password = ref('');
const passwordConfirm = ref('');

const errorMessage = ref('');
const successMessage = ref('');

async function registerUser() {
  errorMessage.value = '';
  successMessage.value = '';

  if (password.value !== passwordConfirm.value) {
    errorMessage.value = 'Пароли не совпадают';
    return;
  }

  const response = await fetch('http://127.0.0.1:8000/auth/register/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      username: name.value,
      email: email.value,
      password: password.value,
      password_confirm: passwordConfirm.value
    })
  }).catch(() => {
    errorMessage.value = 'Не удалось подключиться к серверу';
  });

  if (!response) return;

  if (!response.ok) {
    const err = await response.json().catch(() => null);
    errorMessage.value = err?.detail || 'Ошибка регистрации';
    return;
  }

  successMessage.value = 'Регистрация прошла успешно!';
}
</script>

<template>
  <main class="auth-main">
    <div class="login-card">
      <h1 class="title">Регистрация</h1>

      <div class="input-block">
        <h2>Имя</h2>
        <input v-model="name" type="text" class="auth-input" />
      </div>

      <div class="input-block">
        <h2>Почта</h2>
        <input v-model="email" type="email" class="auth-input" />
      </div>

      <div class="input-block">
        <h2>Пароль</h2>
        <input v-model="password" type="password" class="auth-input" />
      </div>

      <div class="input-block">
        <h2>Подтверждение пароля</h2>
        <input v-model="passwordConfirm" type="password" class="auth-input" />
      </div>

      <button class="nice-button" @click="registerUser">Создать аккаунт</button>

      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </div>
  </main>
</template>

<style scoped>
.auth-main {
  display: flex;
  justify-content: center;
  margin-top: 60px;
}

.login-card {
  border: solid rgb(162, 162, 162) 1px;
  border-radius: 30px;
  padding: 30px 40px;
  width: 360px;
  -webkit-box-shadow: 4px 4px 5px -3px rgba(34, 60, 80, 0.2);
  background: white;
}

.title {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #222222;
  font-size: 32px;
  -webkit-text-stroke: 1px #000;
  text-align: center;
  margin-bottom: 20px;
}

.input-block {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.input-block h2 {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #222222;
  font-size: 22px;
  -webkit-text-stroke: 0.5px #000;
  margin-bottom: 6px;
}

.auth-input {
  width: 100%;
  height: 34px;
  border-radius: 8px;
  border: solid rgb(162, 162, 162) 1px;
  font-size: 16px;
  padding-left: 10px;
}

.nice-button {
  margin-top: 10px;
  width: 100%;
  background: linear-gradient(52deg, rgba(138, 255, 132, 1) 0%, rgba(34, 184, 0, 1) 100%);
  color: white;
  padding: 12px;
  font-size: 22px;
  border-radius: 28px;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px #999;
  transition: transform 0.1s ease, box-shadow 0.1s ease;
}

.nice-button:active {
  transform: scale(0.95);
  box-shadow: 0 0 #666;
}

.error {
  margin-top: 15px;
  color: #ca0000;
  font-size: 16px;
  text-align: center;
}

.success {
  margin-top: 15px;
  color: #00a000;
  font-size: 16px;
  text-align: center;
}
</style>
