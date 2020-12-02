import React from 'react'
//import Form from "bootstrap/Form";
//import { useFormFields } from "../libs/hooksLib";

export default function SignUp() {
    function renderForm() {
        return ( 
        <div class="container">
          <div class="row">
            <div class="col">
              <h2>Sign up</h2>

              <form action = "/api/signup" method="POST">
                  <div class="form-group">
                      <label>Username</label>
                      <input type="text" class="form-control" id="username" name="username" placeholder="Enter a username"/>
                  </div>
                  <div class="form-group">
                      <label>Password</label>
                      <input type="password" class="form-control" id="password" name="password" placeholder="Enter a password"/>
                  </div>
                  <button type="submit" class="btn btn-primary">Sign up</button>
              </form>
            </div>
            <div class="col">
              <h2>Already have an account? Sign in:</h2>
              <form action = "/api/signin" method="POST">
                  <div class="form-group">
                      <label>Username</label>
                      <input type="text" class="form-control" id="username" name="username" placeholder="Enter a username"/>
                  </div>
                  <div class="form-group">
                      <label>Password</label>
                      <input type="password" class="form-control" id="password" name="password" placeholder="Enter a password"/>
                  </div>
                  <button type="submit" class="btn btn-primary">Sign in</button>
              </form>
              </div>
              </div>
            </div>
        );
    }

    return (
        <div className="SignUp">
            <head>
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" 
                    integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous"/>
            </head>
            {renderForm()}
        </div>
    )
}
