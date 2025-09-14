import { NavLink } from "react-router-dom";
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';
import bannerImage from '/src/assets/imgs/Banner.png';

function NavBar() {

    return (
        <Navbar expand="lg" bg="dark" data-bs-theme="dark">
            <Navbar.Toggle aria-controls="navbar-nav" />
            <Navbar.Collapse id="navbar-nav">
                <Nav fill variant="pills">
                    <Nav.Link as={NavLink} to="/add/expense">Add Expense</Nav.Link>
                    <Nav.Link as={NavLink} to="/add/income">Add Income</Nav.Link>
                    <Nav.Link as={NavLink} to="/add/transfer">Add Transfer</Nav.Link>
                    <Nav.Link as={NavLink} to="/add/deposit">Add Deposit</Nav.Link>
                    <Nav.Link as={NavLink} to="/add/currencyrates">Currency Rates</Nav.Link>
                    <Nav.Link as={NavLink} to="/view/acc">View Accounts</Nav.Link>
                    <NavDropdown title="Reports" id="nav-dropdown-reports">
                        <NavDropdown.Item as={NavLink} to="/view/reports/table">View Reports Table</NavDropdown.Item>
                        <NavDropdown.Item as={NavLink} to="/view/reports/year">View Year Report</NavDropdown.Item>
                    </NavDropdown>
                    <NavDropdown title="Options" id="nav-dropdown-options">
                        <NavDropdown.Item as={NavLink} to="/options/db">Database options</NavDropdown.Item>
                        <NavDropdown.Item as={NavLink} to="/options/pb">Accounts options</NavDropdown.Item>
                    </NavDropdown>
                    <Nav.Link as={NavLink} to="/invest">Invest managment</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}


function Banner() {
    return (
        <>
            <img style={{width: '100%', height: 'auto', display: 'block'}} className="banner" src={bannerImage} alt="Acc0unt1ng Banner" />
        </>
    )
}

export default function Header() {
    return (
        <header>
            <Banner />
            <NavBar />
        </header>
    );
}