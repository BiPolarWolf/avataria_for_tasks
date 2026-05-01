
<script setup>

</script>

<template>

  
  <div class="container my-5 mx-auto  bg-purple-600/60 ">
    
    <nav class="py-4">
    <RouterLink class="p-2 bg-purple-300" to="/"> Главная </RouterLink>
    <RouterLink class="p-2 bg-purple-300" to="/about"> О проекте </RouterLink>
    <RouterLink class="p-2 bg-purple-300" to="/profile"> О нас </RouterLink> 
    <RouterLink class="p-2 bg-purple-300" to="/login"> Войти </RouterLink>
    </nav>

    <main class="p-5">
      <RouterView />
    </main>

  </div>

</template>

<style scoped>

</style>