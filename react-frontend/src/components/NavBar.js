import React, { Component } from 'react'
import { Affix, Row, Col, Button, Drawer, Input } from 'antd'


const navButtonStyle = {
  marginTop: '20px',
  color: '#004347',
  fontSize: '16px',
  borderWidth: '2px',
  borderColor: '#004347',
}

class Nav extends Component {
  constructor(props) {
    super(props)
    this.state = { visible: false, top: 0, color: 'white', searchWord: null }
    this.showDrawer = this.showDrawer.bind(this)
    this.onClose = this.onClose.bind(this)
    this.onChange = this.onChange.bind(this)
  }

  showDrawer = () => {
    this.setState({
      visible: true,
    })
  }

  onClose = () => {
    this.setState({
      visible: false,
    })
  }

  onChange = (e) => {
    console.log('input value', e.target.value)
    this.setState({ searchWord: e.target.value })
  }

  render() {
    return (
      <Affix offsetTop={this.state.top}>
        <div
          style={{
            backgroundColor: 'rgb(35, 42, 52)',
            height: '55px',
            boxShadow:
              '0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)',
          }}
        >
          <div>
            <Drawer
              title="選單"
              placement="left"
              closable={false}
              onClose={this.onClose}
              visible={this.state.visible}
              width={'170px'}
              height={'100vh'}
            >
              <Button icon="home" href="/" style={navButtonStyle}>
                Home
              </Button>
              <Button href="/page" style={navButtonStyle}>
                Actions
              </Button>
              <Button href="/" style={navButtonStyle}>
                Up to you
              </Button>
            </Drawer>
          </div>
          <Row type="flex" justify="space-between">
            <Col xs={4} md={2}>
              <Button
                type="dashed"
                size="large"
                icon="menu-unfold"
                onClick={this.showDrawer}
                ghost
                style={{ marginLeft: '6px', marginTop: '7px' }}
              />
            </Col>
          </Row>
        </div>
      </Affix>
    )
  }
}

export default Nav
