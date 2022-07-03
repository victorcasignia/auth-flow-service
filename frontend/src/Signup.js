import './Login.css';
import React from 'react';
import { useForm } from "react-hook-form";
import { Button, Form, ButtonToolbar, Card, Container, Row } from "react-bootstrap";


async function signUp(credentials, onSignIn, setError) {
    return fetch('http://127.0.0.1:8000/api/signup/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    }).then(response => {
        let json = response.json()
        if (response.status >= 200 && response.status < 300) {
            json.then(data => {
                onSignIn()
            })
        }
        else json.then((error) => {
            if (error)
                for (const [key, value] of Object.entries(error)) {
                    if (Array.isArray(value)) {
                        let newValue = value[0]
                        if (newValue === "This field must be unique.") newValue = "Already taken"
                        setError(key, { type: 'custom', message: newValue })
                    }
                }
            else {
                setError('username', { type: 'custom', message: 'Unable to signup user' })
            }
        });
    })
        ;
}

export default function Signup({ onSignIn }) {
    const { register, handleSubmit, watch, formState: { errors }, setError } = useForm();

    const onSubmit = async (data) => {
        await signUp(data, onSignIn, setError);
    }

    return (
        <Container fluid className="vh-100 d-flex flex-column">
            <Row className='w-100 h-100 justify-content-between'>
                <Card style={{ width: '30rem' }} className="text-center m-auto  ml-auto mr-auto">
                    <Card.Body>
                        <Card.Title>Create Account</Card.Title>
                        <Form onSubmit={handleSubmit(onSubmit)}>

                            <Form.Group className="mb-3" controlId="username">
                                <Form.Label>Username</Form.Label>
                                <Form.Control type="text" {...register("username", { required: true })} isInvalid={Boolean(errors.username)} />
                                {errors.username && <Form.Control.Feedback type="invalid">{errors.username.message || "This field is required"}</Form.Control.Feedback>}
                            </Form.Group>

                            <Form.Group className="mb-3" controlId="email">
                                <Form.Label>Email Address</Form.Label>
                                <Form.Control type="text" {...register("email", {
                                    required: true, pattern: {
                                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                                        message: "Invalid email address"
                                    }
                                })} isInvalid={Boolean(errors.email)} />
                                {errors.email && <Form.Control.Feedback type="invalid">{errors.email.message || "This field is required"}</Form.Control.Feedback>}
                            </Form.Group>


                            <Form.Group className="mb-3" controlId="password">
                                <Form.Label>Password</Form.Label>
                                <Form.Control type="password" {...register("password", {
                                    required: true, minLength: {
                                        value: 6,
                                        message: "Must be least 6 characters"
                                    }
                                })} isInvalid={Boolean(errors.password)} />
                                {errors.password && <Form.Control.Feedback type="invalid">{errors.password.message || "This field is required"}</Form.Control.Feedback>}
                            </Form.Group>



                            <Form.Group className="mb-3" controlId="password2">
                                <Form.Label>Password</Form.Label>
                                <Form.Control type="password" {...register("password2", {
                                    required: true, validate: (val) => {
                                        if (watch('password') !== val) {
                                            return "Your passwords do no match";
                                        }
                                    }
                                })} isInvalid={Boolean(errors.password2)} />
                                {errors.password2 && <Form.Control.Feedback type="invalid">{errors.password2.message || "This field is required"}</Form.Control.Feedback>}
                            </Form.Group>


                            <ButtonToolbar className='justify-content-between'>
                                <Button onClick={onSignIn}>Log in</Button>
                                <Button type="submit">Submit</Button>
                            </ButtonToolbar>

                        </Form>
                    </Card.Body>

                </Card>
            </Row>
        </Container>

    );
}