import React, { Component } from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import { Provider } from 'react-redux'
import Main from './components/Main'
import Home from './components/Home'
import Page from './components/Page'
import Navbar from './components/NavBar'
import Send from './components/Send'
import CreateCointype from './components/CreateCointype'
import AddCoin from './components/AddCoin'
import GetBalance from './components/GetBalance'
import AddWallet from './components/AddWallet'
import EXample from './components/Example'

import store from './store'
import './App.css'


class App extends Component {

  render() {    
    return (
      <Provider store={store}>
        <Router>
          <div>
            <Navbar />
            <Main>
              <Switch>
                <Route exact path="/" component={Home} />
                <Route exact path="/page" component={Page} />
                <Route exact path="/send" component={Send} />
                <Route exact path="/createcointype" component={CreateCointype} />
                <Route exact path="/addcoin" component={AddCoin} />
                <Route exact path="/getbalance" component={GetBalance} />
                <Route exact path="/addwallet" component={AddWallet} /> 
                <Route exact path="/example" component={EXample} /> 

              </Switch>
            </Main>
          </div>

        </Router>
      </Provider>
    )
  }
}

export default  App;
