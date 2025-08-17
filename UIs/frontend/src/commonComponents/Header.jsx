import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function NavBar() {
    return (
        <Navbar expand="lg" className="navbar">
            <Container>
                <Navbar.Toggle aria-controls="navbar-nav" />
                <Navbar.Collapse id="navbar-nav">
                    <Nav>
                        <Nav.Link href="/add/expense">Add Expense</Nav.Link>
                        <Nav.Link href="/add/income">Add Income</Nav.Link>
                        <Nav.Link href="/add/transfer">Add Transfer</Nav.Link>
                        <Nav.Link href="/add/deposit">Add Deposit</Nav.Link>
                        <Nav.Link href="/add/currencyrates">Currency Rates</Nav.Link>
                        <Nav.Link href="/view/acc">View Accounts</Nav.Link>
                        <NavDropdown title="Reports" id="nav-dropdown-reports">
                            <NavDropdown.Item href="/view/reports/table">View Reports Table</NavDropdown.Item>
                            <NavDropdown.Item href="/view/reports/year">View Year Report</NavDropdown.Item>
                        </NavDropdown>
                    </Nav>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}


function Banner() {
    return (
        <>
            <img class="banner" src="assets/imgs/Banner.png" alt="Acc0unt1ng Banner" />
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