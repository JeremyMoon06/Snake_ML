import React, { Component } from 'react';

class ResetButton extends Component {

  /* Render reset button */

  render() {
    let resetBoard = this.props.resetBoard;
    return (
      <button id='resetGameButton' className='resetGameButton'
          onClick={resetBoard}>RESET</button>
    )
  }
}

export default ResetButton;