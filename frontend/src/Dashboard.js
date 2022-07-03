import React, { useState, useEffect } from 'react';
import './Dashboard.css';
import { Button, Card, Container, Row, ListGroup } from "react-bootstrap";

async function fetchEndpoint(endpoint, method, token, body, deleteToken, setData) {
  let options = {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + token
    }
  }
  if (method === 'POST')
    options['body'] = JSON.stringify(body)
  return fetch(endpoint, options).then(response => {
    if (response.status === 200) {
      let json = response.json()
      json.then(data => {
        console.log(data)
        if (setData)
          setData(data)
      })
    }
    else if (response.status === 401) {
      deleteToken()
    }
    else {
      deleteToken()
    }
  })
}

function Role(role) {
  return <ListGroup.Item key={role.id}>{role.name}</ListGroup.Item>;
}
function Permission(permission) {
  return <ListGroup.Item key={permission.id}>{permission.name}</ListGroup.Item>;
}

export default function Dashboard({ deleteToken, token, userId }) {
  const [userProfile, setUserProfile] = useState([])
  const [roleList, setRoleList] = useState([])
  const [permissionList, setPermissionList] = useState([])
  useEffect(() => {
    fetchEndpoint(`http://127.0.0.1:8000/api/users/${userId}`, 'GET', token, {}, deleteToken, setUserProfile)
    fetchEndpoint(`http://127.0.0.1:8000/api/users/${userId}/roles`, 'GET', token, {}, deleteToken, setRoleList)
    fetchEndpoint(`http://127.0.0.1:8000/api/users/${userId}/permissions`, 'GET', token, {}, deleteToken, setPermissionList)
  }, [deleteToken, token, userId])

  return (
    <Container fluid className="vh-100 d-flex flex-column">
      <Row className='w-100 h-100 justify-content-between'>
        <Card style={{ width: '30rem' }} className="text-center m-auto  ml-auto mr-auto">


          <Card.Header as='h4' className='d-flex justify-content-between align-items-center"'>
            Welcome {userProfile.username}!
            <Button variant="primary" onClick={deleteToken}>Logout</Button>
          </Card.Header>
          <Card.Body>
            <Card className="text-center">
              <Card.Header as='h5' className='d-flex justify-content-between align-items-center"'>
                Your Roles
              </Card.Header>
              <Card.Body>
                <ListGroup className="scrollbar scrollbar-primary mx-auto" variant="flush">
                  {roleList.map((role) => <Role name={role.name} key={role.id} />)}
                </ListGroup>
              </Card.Body>
            </Card>
            <Card className="text-center">
              <Card.Header as='h5' className='d-flex justify-content-between align-items-center"'>
                Your Permissions
              </Card.Header>
              <Card.Body>
                <ListGroup className="scrollbar scrollbar-primary mx-auto" variant="flush">
                  {permissionList.map((permission) => <Permission name={permission.name} key={permission.id} />)}
                </ListGroup>
              </Card.Body>
            </Card>
          </Card.Body>
        </Card>
      </Row>
    </Container>
  )
}
