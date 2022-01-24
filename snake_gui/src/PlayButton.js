import React, { Component } from 'react';

class PlayButton extends Component {

  /* Render play button */

  render() {
    let playGame = this.props.playGame;
    return (
      <button id='playGameButton' className='playGameButton'
          onClick={playGame}>PLAY</button>
    )
  }
}

export default PlayButton;