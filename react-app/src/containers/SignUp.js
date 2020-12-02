import React from 'react'
import './SignUp.css'

export default function SignUp() {
    return (
        <div class="container">
          <div class="row">
            <div class="col">
              <h2>Sign Up</h2>

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

                <p> Already have an account? <a href="/signin"> Sign in!</a></p>
                </div>
            </div>
        </div>
    )
}
