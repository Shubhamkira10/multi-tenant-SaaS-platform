import { useCallback } from "react";
import TenantLayout from "../../layouts/TenantLayout";
import { fetchEmailLogs } from "../../api/mailApi";
import usePolling from "../../hooks/usePolling";
import "../../assets/css/TablePages.css";

function MailLogs() {
    const getData = useCallback(() => fetchEmailLogs(), []);

    const {
        data: emails = [],
        loading,
        error,
    } = usePolling(getData, 5000);

    if (loading) {
        return (
            <div>
                <h4>Loading...</h4>
            </div>
        );
    }

    if (error) {
        return (
            <div>
                <h4>Failed to load email logs.</h4>
            </div>
        );
    }

    return (
        <div className="page-content">

            <div className="page-header">
                <h2>Email Logs</h2>
                <p>All processed customer emails and their outcomes</p>
            </div>

            <div className="table-container">

                <table className="data-table">

                    <thead>
                        <tr>
                            <th>Provider Message ID</th>
                            <th>Recipient</th>
                            <th>Subject</th>
                            <th>Template</th>
                            <th>Status</th>
                            <th>Sent At</th>
                        </tr>
                    </thead>

                    <tbody>

                        {emails.map((email, index) => (

                            <tr key={email.uuid}>

                                <td className="mono">
                                    {email.provider_message_id || "-"}
                                </td>

                                <td>
                                    {email.recipient}
                                </td>

                                <td>
                                    {email.subject}
                                </td>

                                <td>
                                    {email.template_name || "-"}
                                </td>

                                <td>
                                    <span className="badge badge-processed">
                                        {email.status}
                                    </span>
                                </td>

                                <td>
                                    {email.sent_at || "-"}
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </div>
    );
}

export default MailLogs;