import { useState, useEffect, useCallback } from "react";

export default function usePolling(fetchFn, interval = 5000) {

    const [data, setData] = useState([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    const loadData = useCallback(async () => {

        try {

            const result = await fetchFn();

            setData(result);

            setError(null);

        } catch (err) {

            console.error(err);

            setError(err);

        } finally {

            setLoading(false);

        }

    }, [fetchFn]);

    useEffect(() => {

        loadData();

        const id = setInterval(
            loadData,
            interval
        );

        return () => clearInterval(id);

    }, [loadData, interval]);

    return {
        data,
        loading,
        error,
        reload: loadData,
    };

}