import React, { Component } from "react";
import { Row, Col } from 'antd';
import {withRouter} from "react-router-dom";

class Page extends Component {

  render() {

    return (
      <div style={{ width: "100%", padding: "20px" }}>
        <Row justify="center" type="flex">
        <Col span={8}>
        <br/> 
        </Col>
        </Row>
      </div>
    );
  }
}

const mapStateToProps = state => ({
  state: state.reducerState
});

export default withRouter (Page);
//沒有default 要加{}
//只能export default 一次