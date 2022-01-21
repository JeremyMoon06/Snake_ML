import React, { Component } from 'react'
import ReactDOM from 'react-dom';
import axios from 'axios'
import PlayButton from './PlayButton';
import ResetButton from './ResetButton';

/* Functions for play and reset game live within this component */

class Buttons extends Component {
  /* Timeout list for dynamic gameplay and for efficient resets */
  state = {
    timeoutList: []
  }

  resetTimeoutList = () => {
    this.setState({timeoutList: []})
  }
  
  playGame = () => {
    /* Always reset before current play for instances of current gameplay */
    document.getElementById("resetGameButton").click();
    this.resetTimeoutList();
    let randomNumber = Math.floor(Math.random() * 5);
    /* Do nothing if generation is out of bounds */
    if (this.props.generationNumber < 1 || this.props.generationNumber > 100){return;};
    /* String url based on requested generation number */
    let url = `http://localhost:3001/get/${this.props.generationNumber}`;
    
    axios.get(url).then(response =>{
      /* Fetch reponse with axios based on url */
      let gameplay_list = response.data;
      /* Get current gameplay based on random selection of 5 plays per generation */
      let currentGameplay = gameplay_list[randomNumber];
      let numberOfBoards = currentGameplay.length;
      for (let boardIteration = 0; boardIteration < numberOfBoards; boardIteration++){
        /* Create list of elements that will show the current iteration of the gameplay */
        let listOfElements = [];
        let currentBoard = currentGameplay[boardIteration];
        for (let i = 0; i < 10; i++){
          for (let j = 0; j < 10; j++){
            /* Each element will incement on block within the board */
            let leftPosition = (i * 40 + 4).toString() + "px";
            let topPosition = (j * 40 + 4).toString() + "px";
            /* Each element will be black for open space, yellow for body, and red for target */
            let backgroundColor = "black";
            if (currentBoard[i][j] === 1){
              backgroundColor = "#5FD216";
            }
            if (currentBoard[i][j] === 2){
              backgroundColor = "#C70000";
            }

            /* Define a unique key for each element */
            let elementKey = (i * 10) + j;
            /* Push all elements into list of elements */
            listOfElements.push(
              <div
                key={`element${elementKey}`}
                className='element'
                style={{left: leftPosition, top: topPosition, backgroundColor: backgroundColor}}
                >
              </div>
            );
          }
        }

        /* Set wait time for each frame of the gameplay offset by .1 seconds */
        let waitTime = 100 * boardIteration;

        /* Set the timeout based on wait time for the list of elements for that frame of gameplay */
        let timeout = setTimeout(() => {
          ReactDOM.render(
            <div>
              {listOfElements}
            </div>,
            document.getElementById('board'));
          }, waitTime);

          /* Push timeout to timeout list for potential resets */
          this.state.timeoutList.push(timeout);
      }
    })
  }
  
  resetBoard = () => {
    /* Reset timeoutlist by clearing timeouts then emptying array */
    for (let i = 0; i < this.state.timeoutList.length; i++){
      clearTimeout(this.state.timeoutList[i]);
    }
    let listOfElements = [];

    /* Set all elements within board to black */
    for (let i = 0; i < 10; i++){
      for (let j = 0; j < 10; j++){
        let leftPosition = (i * 40 + 4).toString() + "px";
        let topPosition = (j * 40 + 4).toString() + "px";
        let backgroundColor = "black";
        let elementKey = (i * 10) + j;

        listOfElements.push(
          <div
            key={`element${elementKey}`}
            className='element' 
            style={{left: leftPosition, top: topPosition, backgroundColor: backgroundColor}}
            >
          </div>);
      }
    }

    /* Render black board */
    ReactDOM.render(
      <div>
        {listOfElements}
      </div>,
      document.getElementById('board')
    );
  }

  render() {
    return (
      <div>
        <PlayButton
          playGame={this.playGame}
        />
        <ResetButton
          resetBoard={this.resetBoard}
        />
      </div>
    )
  }
}

export default Buttons;