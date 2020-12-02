import React from 'react'
import './SignIn.css'

export default function SignIn() {
    return (
        <div class="container">
          <div class="row">
            <div class="col">
              <h2>Sign In</h2>

              <form action = "/api/signin" method="POST">
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

                <p> Don't have an account? <a href="/signup"> Sign up!</a></p>
                </div>
            </div>
        </div>
    )
}
