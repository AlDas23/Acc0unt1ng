import {
  BrowserRouter as Router,
  Route,
  Routes
} from "react-router-dom";
import ExpensePage from "./pages/Expense";

export function NavBar() {
  return (
    <Router>
      <nav>
        <Routes>
          <Route path='/' element={<ExpensePage />} >
            <Route path='/add/expense' element={<ExpensePage />} />
            <Route path='/add/expense' element={<IncomePage />} />
            <Route path='/add/transfer' element={<TransferPage />} />
            <Route path='/add/deposit' element={<DepositPage />} />
            <Route path='/currency' element={<CurrencyPage />} />
            <Route path='/view/acc' element={<BalancePage />} />
            <Route path='/view/reports/table' element={<ReportsPage />} />
            <Route path='/view/year' element={<YearPage />} />
            <Route path='/invest' element={<InvestPage />} />
          </Route>
        </Routes>
      </nav>
    </Router>
  );
}
