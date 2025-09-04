import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';

function NavBar() {

    return (
        <Navbar expand="lg" bg="dark" data-bs-theme="dark">
            <Navbar.Toggle aria-controls="navbar-nav" />
            <Navbar.Collapse id="navbar-nav">
                <Nav fill variant="pills">
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
                    <Nav.Link href="/invest">Invest managment</Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
}


function Banner() {
    return (
        <>
            <img style={{width: '100%', height: 'auto', display: 'block'}} className="banner" src="/src/assets/imgs/Banner.png" alt="Acc0unt1ng Banner" />
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