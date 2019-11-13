import React, { Component } from "react";
import { connect } from "react-redux";
import { withRouter } from "react-router-dom";
import { Menu, Dropdown, Icon } from 'antd';


class Layout extends Component {
  constructor(props) {
    super(props);
    this.state = { itemChosen: "" };
    this.chooseItem = this.chooseItem.bind(this);
  }
  chooseItem = (itemContent) => (e) => {
    //this.setState({itemChosen: itemContent})
    this.props.history.push(itemContent)
  }
  render() {
    let renderItems;
    renderItems = this.props.children;
    const menu = (
      <Menu>
        <Menu.Item onClick={this.chooseItem("/addwallet")}>
          Add new wallet!
        </Menu.Item>
        <Menu.Item onClick={this.chooseItem("/createcointype")}>
          Create new cointype!
        </Menu.Item>
        <Menu.Item onClick={this.chooseItem("/addcoin")}>
          Add new coin!
        </Menu.Item>
        <Menu.Item onClick={this.chooseItem("/send")}>
          Send coin!
        </Menu.Item>
        <Menu.Item onClick={this.chooseItem("/getbalance")}>
          GetBalance
        </Menu.Item>       
      </Menu>
    );
    return (
      <main style= {{padding: "20px"}}>
        <Dropdown overlay={menu}>
          <a className="ant-dropdown-link" >
            Actions <Icon type="down" />
          </a>
        </Dropdown>
        <div>{renderItems}</div>
      </main>
    );
  }
}

const mapStateToProps = state => ({
  state: state.reducerState
});
const mapDispatchToProps = dispatch => ({
  dispatchMethod: dispatch
})

export default withRouter(
  connect(
    mapStateToProps,

  )(Layout)
);
