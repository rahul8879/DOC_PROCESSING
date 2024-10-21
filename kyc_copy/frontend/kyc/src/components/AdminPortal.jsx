// React components for an Admin Portal with EY branding and color scheme
import React, { useState } from 'react';
import axios from 'axios';
import { Container, Button, Form, Row, Col, Card, Spinner, Alert, Navbar, Nav } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';


const AdminPortal = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [kycData, setKycData] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      setError('Please upload an image.');
      return;
    }
    setError(null);
    setLoading(true);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8001/extract-kyc-info/', formData);
      setKycData(response.data.data);
    } catch (e) {
      setError('Failed to extract KYC data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar bg="dark" variant="dark" expand="lg" className="mb-5">
        <Container>
          <Navbar.Brand href="#home" style={{ color: '#ffb600' }}>Document AI</Navbar.Brand>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
           
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="admin-portal">
        <Row className="justify-content-center">
          <Col md={8}>
            <Card className="shadow-lg border-0">
              <Card.Header className="text-center" style={{ backgroundColor: '#00338d', color: '#ffffff' }}>
                <h4>Upload KYC Document for Extraction</h4>
              </Card.Header>
              <Card.Body>
                <Form onSubmit={handleSubmit}>
                  <Form.Group controlId="formFile" className="mb-3">
                    <Form.Label>Upload KYC Document Image</Form.Label>
                    <Form.Control type="file" onChange={handleFileChange} />
                  </Form.Group>
                  {error && <Alert variant="danger">{error}</Alert>}
                  <div className="text-center">
                    <Button type="submit" variant="primary" disabled={loading} style={{ backgroundColor: '#ffb600', borderColor: '#ffb600' }}>
                      {loading ? <Spinner as="span" animation="border" size="sm" /> : 'Extract KYC Data'}
                    </Button>
                  </div>
                </Form>
                {kycData && (
                  <div className="kyc-data mt-4">
                    <Card className="border-0">
                      <Card.Body>
                        <h5 className="text-center" style={{ color: '#00338d' }}>Extracted KYC Details</h5>
                        <ul className="list-group list-group-flush">
                          <li className="list-group-item"><strong>Legal Name:</strong> {kycData['Legal Name']}</li>
                          <li className="list-group-item"><strong>Date of Birth:</strong> {kycData['Date of Birth']}</li>
                          <li className="list-group-item"><strong>Nationality:</strong> {kycData['Nationality']}</li>
                          <li className="list-group-item"><strong>Residential Address:</strong> {kycData['Residential Address']}</li>
                          <li className="list-group-item"><strong>Unique Identification Number:</strong> {kycData['Unique Identification Number']}</li>
                        </ul>
                      </Card.Body>
                    </Card>
                  </div>
                )}
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>

      
    </>
  );
};

export default AdminPortal;

// Custom CSS for EY branding in AdminPortal.css
// .admin-portal {
//   font-family: Arial, sans-serif;
//   background-color: #f8f9fa;
//   padding: 20px;
// }
// .card-header, .btn-primary {
//   color: #ffffff;
//   background-color: #00338d;
//   border: none;
// }
// .list-group-item {
//   font-size: 1.1em;
// }
// footer {
//   font-size: 0.9em;
// }
