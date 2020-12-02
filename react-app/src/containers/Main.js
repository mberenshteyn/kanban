import React, { useState, useEffect } from 'react'
import ListGroup from "react-bootstrap/ListGroup";
import { BsPencilSquare } from "react-icons/bs";
import { LinkContainer } from "react-router-bootstrap";
import { useAppContext } from '../libs/contextLib';
import "./Main.css"

export default function Main() {
    const [boards, setBoards] = useState([]);
    const { isLoggedIn } = useAppContext();
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function onLoad() {
            if (!isLoggedIn) {
                return;
            }

            const currBoards = await getBoards();
            setBoards(currBoards);

            setIsLoading(false);
        }

        onLoad();
    }, [isLoggedIn]);

    function renderLander() {
        return (
            <div className ='lander'>
                <h1>Kanban</h1>
                <p className='text-muted'>A tool to structure your projects</p>
            </div>
        )
    }

    function renderBoards() {
        return (
            <div className ='boards'>
                <h2>Boards</h2>
                <ListGroup>{renderBoardList(boards)}</ListGroup> 
            </div>
        )
    }

    async function getBoards() {
        return await fetch('/api/boards', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    return [];
                }
            })
    }

    function renderBoardList(boards) {
        return (
          <>
            <LinkContainer to="/boards/new">
                <ListGroup.Item action>
                <BsPencilSquare size={17} />
                <span className="ml-2 font-weight-bold">Create a new board</span>
                </ListGroup.Item>
            </LinkContainer>
            {boards.map(({ _id, board_name, info }) => ( 
                <LinkContainer key={_id} to={`/boards/${_id}`}>
                    <ListGroup.Item action>
                        <span className="font-weight-bold">
                            {board_name}
                        </span>
                        <br />
                        <span className="text-muted">
                            {info}
                        </span>
                    </ListGroup.Item>
                </LinkContainer>
            ))}
          </>  
        );
    }

    return (
        <div className="Main">
            {isLoggedIn ? renderBoards() : renderLander()}
        </div>
    )
}
