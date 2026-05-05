
<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import Phaser from 'phaser';
import HomeScene from './game/HomeScene';



const gameContainer = ref(null);
let gameInstance = null;

onMounted(() => {
  const config = {
    type: Phaser.AUTO,
    parent: 'phaser-container', // ID элемента выше
    scene: HomeScene,
    scale: {
      mode: Phaser.Scale.RESIZE, // Растягивает канвас под размер родителя
      parent: 'phaser-container',
      width: '100%',
      height: '100%'
    },
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
  width: 100%;
  height: 100%;
  /* Убедитесь, что у родителя этого дива тоже есть высота, 
     иначе 100% от нуля будет нулем */
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

:deep(canvas) {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>