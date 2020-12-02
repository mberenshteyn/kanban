import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import { LinkContainer } from 'react-router-bootstrap'
import Routes from "./Routes"

function App() {
  return (
    <div className="App container py-3">
      <Navbar collapseOnSelect bg="light" expand="md" className="mb-3">
        <LinkContainer to="/">
          <Navbar.Brand className="font-weight-bold">
            Kanban
          </Navbar.Brand>
        </LinkContainer>
        <Navbar.Toggle />
        <Navbar.Collapse className="justify-content-end">
        <Nav activeKey={window.location.pathname}>
            <LinkContainer to="/signup">
              <Nav.Link>Sign up</Nav.Link>
            </LinkContainer>
            <LinkContainer to="/signin">
              <Nav.Link>Sign in</Nav.Link>
            </LinkContainer>
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <Routes />
    </div>
  );
}

export default App;
