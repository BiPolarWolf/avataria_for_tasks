<script setup>
import { reactive, ref } from 'vue';

const formData = reactive({
  username: '',
  password: ''
});

const isLoading = ref(false);
const errorMessage = ref('');

const login = async () => {
  isLoading.value = true;
  errorMessage.value = '';

  try {
    // 1. Формируем данные в формате x-www-form-urlencoded
    const params = new URLSearchParams();
    params.append('username', formData.username);
    params.append('password', formData.password);
    
    // Если в вашей форме OAuth2 требуются дополнительные поля 
    // (например, grant_type, scope, client_id), добавляем их сюда же:
    // params.append('grant_type', 'password');

    // 2. Отправляем запрос
    const response = await fetch('http://localhost:8000/token', {
      method: 'POST',
      headers: {
        // Обязательно указываем правильный Content-Type
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      // Передаем params, никаких JSON.stringify!
      body: params 
    });

    if (!response.ok) {
      throw new Error('Неверный логин или пароль');
    }

    // 3. Получаем ответ с токеном
    const data = await response.json();
    
    // 4. Сохраняем токен (например, в localStorage)
    localStorage.setItem('access_token', data.access_token);
    
    console.log('Успешный вход! Токен:', data.access_token);
    // Здесь обычно делают редирект на защищенную страницу
    // router.push('/dashboard');

  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="form-wrapper">
    <h2>Вход в систему</h2>
    
    <form @submit.prevent="login">
      <div class="input-group">
        <label for="username">Логин:</label>
        <input 
          id="username" 
          v-model="formData.username" 
          type="text" 
          required 
        />
      </div>

      <div class="input-group">
        <label for="password">Пароль:</label>
        <input 
          id="password" 
          v-model="formData.password" 
          type="password" 
          required 
        />
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Вход...' : 'Войти' }}
      </button>
    </form>

    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>


<style scoped>
.form-wrapper {
  max-width: 400px;
  margin: 0 auto;
}
.input-group {
  margin-bottom: 15px;
}
.input-group label {
  display: block;
  margin-bottom: 5px;
}
.input-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}
.error {
  color: red;
  margin-top: 10px;
}
.success {
  color: green;
  margin-top: 10px;
}
</style>