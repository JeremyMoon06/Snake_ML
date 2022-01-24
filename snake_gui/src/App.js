import React, { Component } from 'react'
import './App.css';
import Board from './Board'
import GenerationInput from './GenerationInput';
import GenerationLabel from './GenerationLabel';
import Buttons from './Buttons';

/* Connect database at Snake_ML/server/databaseConnection prior to UI interaction */

class App extends Component {
  /* Generation number as a controlled component within GenerationInput */
  state = {
    generationNumber: 1
  }

  updateGenerationNumber = (event) => {
    this.setState({generationNumber: event.target.value})
  }

/* Render all components */

  render(){
    return (
      <div>
        <Board/>
        <Buttons
          generationNumber={this.state.generationNumber}
        />
        <GenerationLabel/>
        <GenerationInput
          generationNumber={this.state.generationNumber}
          updateGenerationNumber={this.updateGenerationNumber}
        />
      </div>
    );
  }
}

export default App;