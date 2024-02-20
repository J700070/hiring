import {
  EuiBasicTable,
  EuiBasicTableColumn,
  EuiButton,
  EuiLink,
  EuiPageTemplate,
  EuiTableFieldDataColumnType,
} from "@elastic/eui";
import { caseClient, LoaderData } from "../utils";
import { useLoaderData, useNavigate } from "react-router-dom";
import { Case } from "../api/generated";
import "./Dashboard.css";

interface DashboardProps {
  cases: Case[];
}

export function Dashboard() {
  const navigate = useNavigate();

  const { cases } = useLoaderData() as LoaderData<typeof loader>;

  const columns: Array<EuiBasicTableColumn<Case>> = [
    {
      field: "id",
      name: "Id",
      sortable: true,
      truncateText: true,
      render: (id: number) => <>#{id}</>,
      mobileOptions: {
        header: false,
      },
    },
    {
      field: "images",
      name: "Number of Images",
      sortable: true,
      dataType: "number",
      mobileOptions: {
        header: false,
      },
      render: (image: Array<Number>) => image.length,
    },
    {
      field: "open_datetime",
      name: "Open date",
      sortable: true,
      dataType: "date",
      mobileOptions: {
        header: false,
      },
      render: (open_datetime: string) =>
        new Date(open_datetime).toLocaleString(),
    },
    {
      field: "close_datetime",
      name: "Close date",
      sortable: true,
      dataType: "date",
      mobileOptions: {
        header: false,
      },
      render: (close_datetime: string) =>
        close_datetime ? new Date(close_datetime).toLocaleString() : "Open",
    },
  ];

  const getRowProps = (ccase: Case) => {
    const { id } = ccase;
    return {
      "data-test-subj": `row-${id}`,
      className: "customRowClass",
      onClick: () => {
        navigate(`/case/${id}`);
      },
    };
  };

  const getCellProps = (
    ccase: Case,
    column: EuiTableFieldDataColumnType<Case>,
  ) => {
    const { id } = ccase;
    const { field } = column;
    return {
      className: "customCellClass",
      "data-test-subj": `cell-${id}-${String(field)}`,
      textOnly: true,
    };
  };

  const rightSideButtons = [
    <EuiButton
      color="primary"
      iconType="createSingleMetricJob"
      onClick={() =>
        caseClient.caseCreate({}).then((response) => {
          navigate(`/case/${response.data.id}`);
        })
      }
    >
      New Case
    </EuiButton>,
  ];

  return (
    <EuiPageTemplate>
      <EuiPageTemplate.Header
        pageTitle={<span>Dashboard</span>}
        iconType={"eye"}
        rightSideItems={rightSideButtons}
      />
      <EuiPageTemplate.Section>
        <EuiBasicTable
          noItemsMessage={"No cases found. Create a new case to get started."}
          items={cases}
          columns={columns}
          rowHeader="id"
          rowProps={getRowProps}
          cellProps={getCellProps}
          tableLayout="auto"
          className="customTableClass"
        />
      </EuiPageTemplate.Section>
    </EuiPageTemplate>
  );
}

export const loader: ({
  params,
}: {
  params: any;
}) => Promise<DashboardProps> = async ({ params }) => {
  const { data: cases } = await caseClient.caseList();
  return { cases };
};
