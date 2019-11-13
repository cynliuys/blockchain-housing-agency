import React, { Component } from 'react';
import axios from 'axios'

const axiosConfigGet = {
   method: "get",
}
const axiosConfigPost = {
   method: "post",
   url: "http://127.0.0.1:5000/post"
}

class EXample extends Component {
   constructor(props) {
      super(props);
      this.state = {entry: ""};
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
      this.handleSubmitPost = this.handleSubmitPost.bind(this);
   }
   handleChange = (event) => {
      this.setState({
        [event.target.id]: event.target.value,
      })
    }
    handleSubmit = () => {
      axios({...axiosConfigGet, url: `http://127.0.0.1:5000/store/${this.state.entry}`})
         .then((res)=>{
            console.log(`response from the server is ${res}`)
            this.setState((prevState)=>({...prevState, store: res.data.name}))
         })
         .catch((err)=>{
            console.log(`error connecting the server is ${err}`)
         })
    }
    handleSubmitPost = () => {
      axios({...axiosConfigPost, data: {entry: this.state.entry}})
      .then((res)=>{
         console.log(`response from the server is ${res}`)
      })
      .catch((err)=>{
         console.log(`error connecting the server is ${err}`)
      })
    }
   render() {
      return (
         <div>
            <label htmlFor="entry">Entry :</label>
            <input
               type="text"
               id="entry"
               placeholder="標題..."
               value={this.state.entry}
               onChange={this.handleChange}
            />
            <br /><br />
            <button onClick={this.handleSubmit}>submit</button>
            <button onClick={this.handleSubmitPost}>post</button>

            <h4>data from server</h4>
            <p>{this.state.store}</p>
         </div>
      );
   }
}

export default EXample;