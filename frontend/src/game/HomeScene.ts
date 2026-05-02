import Phaser from 'phaser';

export default class HomeScene extends Phaser.Scene {
  // 1. Объявляем свойства класса вне конструктора для типизации
  private items: Phaser.GameObjects.Rectangle[];

  constructor() {
    super('HomeScene');
    this.items = []; // Теперь TS знает, что это массив прямоугольников
  }

  preload(): void {
    // Рекомендуется указывать возвращаемый тип функций (: void)
    this.load.image('room', 'https://labs.phaser.io/assets/skies/space3.png');
    // Исправьте путь, если музыка не грузится
    this.load.audio('music',['assets/audio/music.mp3']);
  }

  create(): void {
    // Фон комнаты
    this.add.image(500, 500, 'room').setScale(2);

    this.sound.add('music').play({
         loop : true   
        })


    // Текст-приветствие
    this.add.text(20, 20, "Мой Уютный Дом", {
      fontSize: '24px',
      color: '#ffffff' // В объекте стилей текста лучше использовать 'color' вместо 'fill'
    });

    // 2. Слушаем событие. Чтобы TS не ругался на game.events, 
    // можно использовать eventEmitter сцены или привести типы
    this.game.events.on('addItem', (itemType: string) => {
      this.addNewItem(itemType);
    });
  }

  // 3. Указываем тип для аргумента itemType
  addNewItem(itemType: string): void {
    const x = Phaser.Math.Between(100, 700);
    const y = Phaser.Math.Between(100, 500);
    
    const rect = this.add.rectangle(x, y, 50, 50, 0x00ff00);
    this.add.text(x - 20, y - 40, itemType, { fontSize: '12px' });
    
    this.items.push(rect);
  }
}