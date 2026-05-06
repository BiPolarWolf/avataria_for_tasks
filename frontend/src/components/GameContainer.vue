
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import Phaser from 'phaser';
import HomeScene from '../game/HomeScene.js'
import { Input } from 'postcss';


const gameContainer = ref(null);
let gameInstance = null;

onMounted(() => {
  const config = {
    type: Phaser.AUTO,
    parent: 'phaser-container', // ID элемента выше
    width: 500,
    height: 500,
    scene: HomeScene,
    physics: {
      default: 'arcade',
      arcade: { debug : false}
    },
  };

  gameInstance = new Phaser.Game(config);
});


// Удаляем игру при закрытии компонента, чтобы не тратить память
onUnmounted(() => {
  if (gameInstance) {
    gameInstance.destroy(true);
  }
});

</script>

<template>
    <div id="phaser-container" ref="gameContainer"></div>
</template>


<style scoped>


#phaser-container {

}

.ui-panel {
  padding: 20px;
  background: #f0f0f0;
  border-radius: 10px;
}

</style>