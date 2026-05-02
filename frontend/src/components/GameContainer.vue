
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import Phaser from 'phaser';
import HomeScene from '../game/HomeScene.js'

const gameContainer = ref(null);
let gameInstance = null;

onMounted(() => {
  const config = {
    type: Phaser.AUTO,
    parent: 'phaser-container', // ID элемента выше
    width: 1000,
    height: 700,
    scene: HomeScene,
    physics: {
      default: 'arcade',
      arcade: { gravity: { y: 0 } }
    }
  };

  gameInstance = new Phaser.Game(config);
});

// Метод для покупки
const buyFurniture = (name) => {
  if (gameInstance) {
    // Отправляем событие внутрь Phaser
    gameInstance.events.emit('addItem', name);
  }
};

// Удаляем игру при закрытии компонента, чтобы не тратить память
onUnmounted(() => {
  if (gameInstance) {
    gameInstance.destroy(true);
  }
});

</script>

<template>
  <div class="game-wrapper">
    <!-- Контейнер, куда Phaser "вставит" игру -->
    <div id="phaser-container" ref="gameContainer"></div>
    
    <div class="ui-panel">
      <h3>Магазин мебели</h3>
      <button @click="buyFurniture('Кровать')">Купить Кровать (100$)</button>
      <button @click="buyFurniture('Стул')">Купить Стул (50$)</button>
    </div>
  </div>
</template>


<style scoped>
.game-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

#phaser-container {
  border: 4px solid #42b983;
  border-radius: 8px;
  overflow: hidden;
}

.ui-panel {
  padding: 20px;
  background: #f0f0f0;
  border-radius: 10px;
}

button {
  margin: 5px;
  padding: 10px;
  cursor: pointer;
}
</style>