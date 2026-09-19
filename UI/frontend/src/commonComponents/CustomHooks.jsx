import { useState, useEffect, useCallback } from 'react';

// Custom hook to detect screen size
const useIsMobile = (breakpoint = 768) => {
    const [isMobile, setIsMobile] = useState(false);

    useEffect(() => {
        const checkScreenSize = () => {
            setIsMobile(window.innerWidth < breakpoint);
        };

        checkScreenSize();
        window.addEventListener('resize', checkScreenSize);

        return () => window.removeEventListener('resize', checkScreenSize);
    }, [breakpoint]);

    return isMobile;
};

const useOptions = (apiType) => {
    const [options, setOptions] = useState(null);
    const [error, setError] = useState(null);

    const fetchOptions = useCallback(async () => {
        try {
            setError(null);

            const response = await fetch(`/api/get/options/${apiType}`);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            if (data.redirect) {
                alert('Database is missing or corrupted. You will be redirected to the setup page.');
                window.location.href = data.redirect;
                return;
            }

            if (data.success) {
                setOptions(data.options);
            } else {
                throw new Error(data.message || 'Failed to load options');
            }
        } catch (err) {
            console.error(`Error fetching ${apiType} options:`, err);
            setError(err.message || 'Unexpected error occurred while fetching options');
            alert('Unexpected error occurred while fetching options: ' + err.message);
        }
    }, [apiType]);

    useEffect(() => {
        fetchOptions();
    }, [fetchOptions]);

    return { options, error };
}

const useHistory = (apiType, year) => {
    const [history, setHistory] = useState(null);
    const [error, setError] = useState(null);

    const fetchHistory = useCallback(async () => {
        try {
            setError(null);

            var response;
            if (year === null) {
                response = await fetch(`/api/get/history/${apiType}`);
             } else {
                response = await fetch(`/api/get/history/${apiType}/${year}`);
            }
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();

            if (data.redirect) {
                alert('Database is missing or corrupted. You will be redirected to the setup page.');
                window.location.href = data.redirect;
                return;
            }

            if (data.success) {
                setHistory(data.history);
            } else {
                throw new Error(data.message || 'Failed to load history');
            }
        } catch (err) {
            console.error(`Error fetching ${apiType} history:`, err);
            setError(err.message || 'Unexpected error occurred while fetching history');
            alert('Unexpected error occurred while fetching history: ' + err.message);
        }
    }, [apiType, year]);

    useEffect(() => {
        fetchHistory();
    }, [fetchHistory]);

    return { history, error };
}

export { useIsMobile, useOptions, useHistory };