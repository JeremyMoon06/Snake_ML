import React, { Component } from 'react';

class ResetButton extends Component {

  /* Button information for reset */

  render() {
    let resetBoard = this.props.resetBoard;
    return (
      <button id='resetGameButton' className='resetGameButton'
          onClick={resetBoard}>RESET</button>
    )
  }
}

export default ResetButton;