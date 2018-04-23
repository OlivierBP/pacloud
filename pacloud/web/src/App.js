import React, { Component } from 'react';
import {Navbar,FormGroup,FormControl, Button} from 'react-bootstrap';
import logo from './logo.svg';
import Packages from './Packages';
import './App.css';
require("react-bootstrap/lib/NavbarHeader");


class App extends Component {

  render() {
    return (
      <div className="App">
	<header className="App-header">
	  <img src={logo} className="App-logo" alt="logo" />
	  <h1 className="App-title">Welcome to Pacloud</h1>
	</header>

	<Navbar>

	  <Navbar.Header>
	    <Navbar.Brand> <p>Pacloud</p> </Navbar.Brand>
	    <Navbar.Toggle />
	  </Navbar.Header>

	  <Navbar.Collapse>
	    <Navbar.Form pullRight>
		    <FormGroup>
		      <FormControl type="text" placeholder="Search" />
		    </FormGroup>{' '}
		    <Button type="submit">Submit</Button>
	    </Navbar.Form>
	  </Navbar.Collapse>
	</Navbar>
	<Packages/>
      </div>
    );
  }
};
export default App;
