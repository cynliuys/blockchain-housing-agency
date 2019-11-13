import React, { Component } from "react";
import axios from 'axios'


const axiosConfigGet = {
  method: "get",
}
const axiosConfigPost = {
  method: "post",
  url: "http://127.0.0.1:5000/post"
}

class GetBalance extends Component {
  constructor(props) {
    super(props);
    this.state = {
      username: '',
      balance: ''
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({
      [event.target.id]: event.target.value,
    })
  }

  handleSubmit = () => {
    axios({ ...axiosConfigGet, url: `http://127.0.0.1:5000/actions/gb/${this.state.username}` })
      .then((res) => {
        console.log(`response from the server is ${res}`)
        this.setState((prevState) => ({ ...prevState, balance: res.data.balance }))
      })
      .catch((err) => {
        console.log(`error connecting the server is ${err}`)
      })
  }

  render() {
    return (
      <div>
        <br />
        <h1 className="display-4 text-center mt-4"> Get Balance! </h1>
        <h3 className="lead text-center">帳戶餘額查詢</h3>
        <br />
        <label htmlFor="title"> Username : </label>
        <input
          type="text"
          className="form-control"
          id="username"
          placeholder="Name of the user"
          value={this.state.username}
          onChange={this.handleChange}
          required
        />
        <br /><br />
        <button onClick={this.handleSubmit}>submit</button>
        <br /><br />

        <h2>{this.state.balance}</h2>
      </div>
    )
  }
}

export default GetBalance;