import React, { useState, useEffect } from 'react'
import './App.css';
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import { LinkContainer } from 'react-router-bootstrap'
import Cookies from 'js-cookie'
import { useHistory } from 'react-router-dom'
import Routes from './Routes'
import { AppContext } from './libs/contextLib'

function App() {
  const history = useHistory();
  const [isLoggedIn, userHasLoggedIn] = useState(false);

  useEffect(() => {onLoad();}, [])

  function onLoad() {
    console.log("checking if logged in");
    console.log(Cookies.get('session'))
    if (Cookies.get('session')) {
      userHasLoggedIn(true);
      console.log("verifying user is logged in");
    }
  }

  function handleSignOut() {
    userHasLoggedIn(false);
    fetch('/api/signout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    history.push("/signin");
  }

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
          {isLoggedIn ? (
              <Nav.Link onClick={handleSignOut}>Sign Out</Nav.Link>
            ) : (
              <>
                  <LinkContainer to="/signup">
                    <Nav.Link>Sign up</Nav.Link>
                  </LinkContainer>
                  <LinkContainer to="/signin">
                    <Nav.Link>Sign in</Nav.Link>
                  </LinkContainer>
            </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Navbar>
      <AppContext.Provider value ={{isLoggedIn, userHasLoggedIn}}>
        <Routes />
      </AppContext.Provider>
    </div>
  );
}

export default App;
