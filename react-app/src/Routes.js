import React from 'react'
import { Route, Switch } from "react-router-dom";
import Main from "./containers/Main";
import SignUp from "./containers/SignUp"
import SignIn from "./containers/SignIn"
import NewBoard from "./containers/NewBoard"

export default function Routes() {
    return (
        <Switch>
            <Route exact path="/">
                <Main />
            </Route>
            <Route exact path="/signup">
                <SignUp />
            </Route>
            <Route exact path="/signin">
                <SignIn />
            </Route>
            <Route exact path="/boards/new">
                <NewBoard />
            </Route>
        </Switch>
    );
}
