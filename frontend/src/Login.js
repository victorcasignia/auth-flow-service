import './Login.css';
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import { useForm } from "react-hook-form";
import Signup from './Signup';
import { Button, Form, ButtonToolbar, Card, Container, Row } from "react-bootstrap";


async function loginUser(credentials, setError, setToken) {
  return fetch('http://127.0.0.1:8000/api/login/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  }).then(response => {
    if (response.status === 200) {
      let json = response.json()
      json.then(data => {
        setToken(data)
      })
    }
    else throw new Error(response.status);
  })
    .catch(error => {
      setError("username", { type: 'custom', message: "Invalid Credentials" })
      setError("password", { type: 'custom', message: "Invalid Credentials" })
    });
}

export default function Login({ setToken }) {
  const { register, handleSubmit, formState: { errors }, setError, reset } = useForm();
  const [isSignup, setIsSignup] = useState(false)
  const onSubmit = async (data) => {
    await loginUser(data, setError, setToken);
  }

  const onSignUp = () => {
    reset()
    setIsSignup(true)
  }

  const onSignIn = () => {
    setIsSignup(false)
  }

  if (isSignup) {
    return <Signup onSignIn={onSignIn} />
  }

  else
    return (
      <Container fluid className="vh-100 d-flex flex-column">
        <Row className='w-100 h-100 justify-content-between'>
          <Card style={{ width: '30rem' }} className="text-center m-auto  ml-auto mr-auto">
            <Card.Body>
              <Card.Title>Login</Card.Title>
              <Form onSubmit={handleSubmit(onSubmit)}>
                <Form.Group className="mb-3" controlId="username">
                  <Form.Label>Username or Email Address</Form.Label>
                  <Form.Control type="text" {...register("username", { required: true })} isInvalid={Boolean(errors.username)} />
                  {errors.username && <Form.Control.Feedback type="invalid">{errors.username.message || 'This field is required'}</Form.Control.Feedback>}
                </Form.Group>
                <Form.Group className="mb-3" controlId="password">
                  <Form.Label>Password</Form.Label>
                  <Form.Control type="password" {...register("password", { required: true })} isInvalid={Boolean(errors.password)} />
                  {errors.password && <Form.Control.Feedback type="invalid">{errors.password.message || 'This field is required'}</Form.Control.Feedback>}
                </Form.Group>
                <ButtonToolbar className='justify-content-between'>
                  <Button onClick={onSignUp}>Sign up</Button>
                  <Button type="submit">Submit</Button>
                </ButtonToolbar>
              </Form>
            </Card.Body>
          </Card>
        </Row>
      </Container>

    );
}

Login.propTypes = {
  setToken: PropTypes.func.isRequired
}