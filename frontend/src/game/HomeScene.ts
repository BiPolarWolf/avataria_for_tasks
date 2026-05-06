import Phaser from 'phaser';
import { Player , type PlayerConfig } from './Player';
export default class HomeScene extends Phaser.Scene {
  player !: Player
  background !: Phaser.GameObjects.TileSprite
  cursors !: Phaser.Types.Input.Keyboard.CursorKeys

  constructor() {
    super('HomeScene');
  }

  preload(): void {


    // Рекомендуется указывать возвращаемый тип функций (: void)
    this.load.image('room', 'https://labs.phaser.io/assets/skies/space3.png');
    // Исправьте путь, если музыка не грузится
    this.load.audio('music',['assets/audio/music.mp3']);
    // 'bg_square' — это ключ, по которому мы будем обращаться к картинке
    this.load.image('wood_floor', 'assets/images/wood_floor.png');

    this.load.image('player','assets/images/player1.png')

  }

  create(): void {

    const width = 1000
    const height = 800

    const roomWidth = 1200;
    const roomHeight = 1200;



    const config : PlayerConfig = {
      scene : this,
      position : {x:width/2,y:height/2},
      assetKey : 'player',
      frame : 1

    }

    this.background = this.add.tileSprite(0,0,roomWidth,roomHeight,'wood_floor')

    this.background.setOrigin(0,0);
    this.background.setTileScale(0.5);


    this.physics.world.setBounds(0,0,roomWidth,roomHeight);
    this.cameras.main.setBounds(0, 0, roomWidth, roomHeight);


    this.player = new Player(config);



    (this.player.body as Phaser.Physics.Arcade.Body).setCollideWorldBounds(true);

    this.cameras.main.startFollow(this.player,true, 0.1, 0.1)
    this.cameras.main.setZoom(1.5); // Чуть приблизим для уюта


    if (this.input.keyboard) {
        this.cursors = this.input.keyboard.addKeys({
          up: Phaser.Input.Keyboard.KeyCodes.UP,
          down: Phaser.Input.Keyboard.KeyCodes.DOWN,
          left: Phaser.Input.Keyboard.KeyCodes.LEFT,
          right: Phaser.Input.Keyboard.KeyCodes.RIGHT,
        }) as Phaser.Types.Input.Keyboard.CursorKeys;
    }

  }

  update (){

    const speed = 400

    this.player.setVelocity(0)

  // Обработка ввода
        if (this.cursors.left.isDown) {
            this.player.setVelocityX(-speed);
        } else if (this.cursors.right.isDown) {
            this.player.setVelocityX(speed);
        }

        if (this.cursors.up.isDown) {
            this.player.setVelocityY(-speed);
        } else if (this.cursors.down.isDown) {
            this.player.setVelocityY(speed);
        }

    // тут будет какой то код

  }

}
