import React, { useState } from 'react'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Alert from 'react-bootstrap/Alert'
import { useAppContext } from "../libs/contextLib"
import './SignUp.css'

export default function SignUp() {
    const { userHasLoggedIn } = useAppContext();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [success, setSuccess] = useState(0)
    const [show, setShow] = useState(true);

    function validateForm() {
        return username.length >= 5 && password.length >= 5;
    }

    function validatePasswords() {
        return password === confirmPassword;
    }

    function handleInvalidInput() {
        if (show) {
            return (
                <Alert variant="danger" onClose={() => setShow(false)} dismissible>
                    <b>This account already exists.</b><br></br>
                    Please try a different username.
                </Alert>
            );
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        fetch('/api/signup', {
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
                } else {
                    setShow(true);
                    setSuccess(1);
                }
        })
    }

    return (
        <div className="SignUp">
            <h1>Sign Up</h1>
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
                <Form.Group size="lg" controlId="confirmPassword">
                    <Form.Label>Confirm Password</Form.Label>
                    <Form.Control 
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                </Form.Group>
                {!validateForm() && <Alert variant="warning"><b>Note: </b>Username and password must each be at least five characters long.</Alert>}
                {!validatePasswords() && <Alert variant="warning"><b>Note: </b>Passwords do not match.</Alert>}
                {success === 1 && handleInvalidInput()}
                <Button block size="lg" type="submit" disabled={!validateForm() || !validatePasswords()}>
                    Sign Up
                </Button>
            </Form>
            <p>Already have an account? <a href="/signin">Sign in</a> instead.</p>
        </div>
    )
}
