import React, { Component } from 'react';

class GenerationInput extends Component {

  /* Controlled component for generation input */

  render() {
    return (
      <input
        className='generationInput'
        id="generation"
        name="generation"
        type="text" 
        value={this.props.generationNumber}
        onChange={this.props.updateGenerationNumber}
      >
      </input>
    )
  }
}

export default GenerationInput;