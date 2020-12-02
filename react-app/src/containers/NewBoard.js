import React, { useState } from 'react'
import Form from 'react-bootstrap/Form'
import Alert from 'react-bootstrap/Alert'
import Button from 'react-bootstrap/Button'
import { useHistory } from 'react-router-dom'
import "./NewBoard.css"

export default function NewBoard() {
    const history = useHistory();
    const [title, setTitle] = useState("");
    const [content, setContent] = useState("");
    const [success, setSuccess] = useState(0)
    const [show, setShow] = useState(true);

    function validateForm() {
        return title.length > 0 && content.length > 0;
    }

    function handleInvalidInput() {
        if (show) {
            return (
                <Alert variant="danger" onClose={() => setShow(false)} dismissible>
                    <b>You already have a board with this name.</b><br></br>
                    Please try a different name.
                </Alert>
            );
        }
    }

    function handleSubmit(event) {
        event.preventDefault();
        fetch('/api/boards/new', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
              },
            body: JSON.stringify({board_name: title, info: content}),
        }).then(response => {
            if (response.ok) {
                setSuccess(2);
                history.push('/');
            } else {
                setShow(true);
                setSuccess(1);
            }
        })
    }

    return (
        <div className="NewBoard">
            <Form onSubmit={handleSubmit}>
                <Form.Group controlID="title">
                    <Form.Label>Name</Form.Label>
                    <Form.Control
                        autoFocus
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                    />
                </Form.Group>
                <Form.Group controlID="content">
                    <Form.Label>Details</Form.Label>
                    <Form.Control
                        value={content}
                        as="textarea"
                        onChange={(e) => setContent(e.target.value)}
                    />
                </Form.Group>
                {!validateForm() && <Alert variant="warning"><b>Note: </b>Name and details cannot be empty!</Alert>}
                {success === 1 && handleInvalidInput()}
                <Button block size="lg" type="submit" disabled={!validateForm()}>
                    Create
                </Button>
            </Form>
        </div>
    )
}
