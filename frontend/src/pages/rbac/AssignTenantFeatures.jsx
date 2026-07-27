import { useEffect, useState } from "react";

import { getTenants } from "../../api/tenantApi";
import { getFeatures } from "../../api/featureApi";
import {
    assignFeatureToTenant,
    getTenantFeatures,
} from "../../api/rbacApi";

function AssignTenantFeatures() {

    const [tenants, setTenants] = useState([]);
    const [features, setFeatures] = useState([]);

    const [tenantUuid, setTenantUuid] = useState("");

    const [selectedFeatures, setSelectedFeatures] = useState([]);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {

        const tenantRes = await getTenants();
        const featureRes = await getFeatures();

        setTenants(tenantRes.data);
        setFeatures(featureRes.data);

    };

    const loadTenantFeatures = async (uuid) => {

        const response = await getTenantFeatures(uuid);

        const assigned = response.data.map(
            (item) => item.feature_uuid
        );

        setSelectedFeatures(assigned);

    };

    const handleTenantChange = (e) => {

        const uuid = e.target.value;

        setTenantUuid(uuid);

        if (uuid) {
            loadTenantFeatures(uuid);
        }

    };

    const handleCheckbox = (featureUuid) => {

        if (selectedFeatures.includes(featureUuid)) {

            setSelectedFeatures(
                selectedFeatures.filter(
                    (id) => id !== featureUuid
                )
            );

        } else {

            setSelectedFeatures([
                ...selectedFeatures,
                featureUuid,
            ]);

        }

    };

    const handleAssign = async () => {

        for (const featureUuid of selectedFeatures) {

            await assignFeatureToTenant({
                tenant_uuid: tenantUuid,
                feature_uuid: featureUuid,
            });

        }

        alert("Features Assigned Successfully");

    };

    return (

        <div className="container">

            <h3 className="mb-4">
                Assign Features To Tenant
            </h3>

            <select
                className="form-select mb-4"
                value={tenantUuid}
                onChange={handleTenantChange}
            >

                <option value="">
                    Select Tenant
                </option>

                {tenants.map((tenant) => (

                    <option
                        key={tenant.uuid}
                        value={tenant.uuid}
                    >
                        {tenant.name}
                    </option>

                ))}

            </select>

            {features.map((feature) => (

                <div
                    key={feature.uuid}
                    className="form-check mb-2"
                >

                    <input
                        type="checkbox"
                        className="form-check-input"
                        checked={selectedFeatures.includes(
                            feature.uuid
                        )}
                        onChange={() =>
                            handleCheckbox(feature.uuid)
                        }
                    />

                    <label className="form-check-label">

                        {feature.name}

                    </label>

                </div>

            ))}

            <button
                className="btn btn-primary mt-4"
                onClick={handleAssign}
            >
                Assign Features
            </button>

        </div>

    );

}

export default AssignTenantFeatures;