import React, { useState } from 'react'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'
import { useHistory } from 'react-router-dom'
import { useAppContext } from "../libs/contextLib"
import './SignIn.css'

export default function SignIn() {
    const history = useHistory();
    const { userHasLoggedIn } = useAppContext();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [success, setSuccess] = useState(0)
    const [show, setShow] = useState(true);

    function validateForm() {
        return username.length >= 5 && password.length >= 5;
    }

    function handleInvalidInput() {
        if (show) {
            return (
                <Alert variant="danger" onClose={() => setShow(false)} dismissible>
                    <b>Incorrect username or password!</b>
                    <br></br>
                    Please try again.
                </Alert>
            );
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        fetch('/api/signin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
              },
            body: JSON.stringify({username: username, password: password}),
        }).then(response => {
            return response.json()
        }).then(json => {
                console.log(json);
                if (json["authenticated"]) {
                    userHasLoggedIn(true);
                    setSuccess(2);
                    history.push('/');
                } else {
                    setShow(true);
                    setSuccess(1);
                }
        })
    }

    return (
        <div className="SignIn">
            <h1>Sign In</h1>
            <Form onSubmit={handleSubmit}>
                <Form.Group size="lg" controlId="username">
                    <Form.Label>Username</Form.Label>
                    <Form.Control
                        autoFocus
                        type="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                    />
                </Form.Group>
                <Form.Group size="lg" controlId="password">
                    <Form.Label>Password</Form.Label>
                    <Form.Control 
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </Form.Group>
                {success === 1 && handleInvalidInput()}
                <Button block size="lg" type="submit" disabled={!validateForm()}>
                    Sign In
                </Button>
            </Form>
            <p>Don't have an account? <a href="/signup">Sign up</a> today.</p>
        </div>
    )
}
