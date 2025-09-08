import { useState, useEffect } from "react";
import Header from "../commonComponents/Header";
import Button from "react-bootstrap/esm/Button";

export function OptionsPB() {
    // TODO: Implement Person-Bank set-up page
}

export function OptionsDB() {
    const [currentLists, setCurrentLists] = useState({ curr: [], incCat: [], expCat: [], subCat: [] });
    const [isDBExists, setIsDBExists] = useState();

    useEffect(() => {
        // TODO: Fetch SPVs from backend and DB status
    }, []);

    // TODO: Implement validation and save functionality

    return (
        <>
            <Header />
            <div className="options-page container">
                <div className="row">
                    <h2>Special Values Control</h2>
                    <Form id="spv-form" > 
                        <div className="col">
                            <label htmlFor="currency-values">Currency Values</label>
                            {currentLists &&
                                (<textarea form="spv-form" id="currency-values" name="currency-values" rows="25" cols="30">
                                    {currentLists.curr.join("\n")}
                                </textarea>)}
                            <br />
                            <Button variant="primary" type="submit">
                                Save Changes
                            </Button>
                        </div>
                        <div className="col">
                            <label htmlFor="inccat-values">Income Category Values</label>
                            {currentLists &&
                                (<textarea form="spv-form" id="inccat-values" name="inccat-values" rows="25" cols="30">
                                    {currentLists.incCat.join("\n")}
                                </textarea>)}
                        </div>
                        <div className="col">
                            <label htmlFor="expcat-values">Expense Category Values</label>
                            {currentLists &&
                                (<textarea form="spv-form" id="expcat-values" name="expcat-values" rows="25" cols="30">
                                    {currentLists.expCat.join("\n")}
                                </textarea>)}
                        </div>
                        <div className="col">
                            <label htmlFor="subcat-values">Subcategory Values</label>
                            {currentLists &&
                                (<textarea form="spv-form" id="subcat-values" name="subcat-values" rows="25" cols="30">
                                    {currentLists.subCat.join("\n")}
                                </textarea>)}
                        </div>
                    </Form>
                </div>
                <div className="row">
                    <h2>Database Control</h2>
                    {/* TODO: Create DB control option (creation, replacement, etc.) */}
                </div>
            </div>
        </>
    )
}