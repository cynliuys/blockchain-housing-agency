import React, { Component } from "react";
import axios from 'axios'

const axiosConfigGet = {
  method: "get",
}
const axiosConfigPost = {
  method: "post",
  url: "http://127.0.0.1:5000/post"
}

class Send extends Component {
  constructor(props) {
    super(props);
    this.state = {
      from_addr: '',
      to_addr: '',
      cointype: '',
      amount: '',
      status: ''
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
    axios({ ...axiosConfigGet, url: `http://127.0.0.1:5000/actions/s/${this.state.from_addr}/${this.state.to_addr}/${this.state.cointype}/${this.state.amount}` })
      .then((res) => {
        console.log(`response from the server is ${res}`)
        this.setState((prevState) => ({ ...prevState, status: res.data.status }))
      })
      .catch((err) => {
        console.log(`error connecting the server is ${err}`)
      })
  }

  render() {
    return (
      <div >
        <br />
        <h1 className="display-4 text-center mt-4"> Send Coins to Someone  </h1>
        <h3 className="lead text-center">區塊鏈交易！</h3>
        <br />
        <label htmlFor="title"> Sender : </label>
        <input
          type="text"
          className="form-control"
          id="from_addr"
          placeholder="Address of the sender"
          value={this.state.from_addr}
          onChange={this.handleChange}
          required
        />
        <br /><br />
        <label htmlFor="tags">Receiver : </label>
        <input
          type="text"
          className="form-control"
          id="to_addr"
          placeholder="Address of the receiver"
          value={this.state.to_addr}
          onChange={this.handleChange}
          required
        />
        <br /><br />
        <label htmlFor="tags">Cointype : </label>
        <input
          type="text"
          className="form-control"
          id="cointype"
          placeholder="Type of the coin"
          value={this.state.cointype}
          onChange={this.handleChange}
          required
        />
        <br /><br />
        <label htmlFor="tags">Amount : </label>
        <input
          type="number"
          className="form-control"
          id="amount"
          placeholder="Amount of coin to transfer"
          value={this.state.amount}
          onChange={this.handleChange}
          required
        />
        <br /><br />
        <button onClick={this.handleSubmit}>submit</button>
        <br /><br />
        <h2>{this.state.status}</h2>

      </div>
    )
  }
}
export default Send;