import { useState } from "react"

import { get_user_labels, delete_user_label } from "../../backendapi"

import { Row, Spinner, Button, Dropdown, ButtonGroup } from "react-bootstrap"
import AddLabelModal from "./AddLabelModal";


function Label(props)
{
    const { label, choosen, click_callback, label_delete_callback } = props;

    return (<>
    <Row style={{padding: "10px 20px"}} >
    <Dropdown as={ButtonGroup}>
        <Button 
            className="text-start" 
            variant={ (choosen ? "" : "outline-") + "secondary" }
            onClick={ choosen ? null : () => { click_callback(label, "active") } }
            style={{width: "100%"}}
        >
            <i className="bi bi-tag-fill"></i>
            <span>
                { " " + label }
            </span>
        </Button>

      <Dropdown.Toggle split variant="outline-secondary" id="dropdown-split-basic" />

      <Dropdown.Menu>
        <Dropdown.Item onClick={ () => label_delete_callback(label) }>Delete label</Dropdown.Item>
        <Dropdown.Divider />
        <Dropdown.Item disabled>All notes with this label will remain, the label will just be removed from them</Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
    </Row>
    </>);
}


let label_list = [];
let lables;

/* Component states
    loading
    rerender
*/
function LabelChooser(props)
{
    const main_page_config = 
        localStorage.getItem("main_page_config") === null ? 
        { notes_label: "", notes_status: "active"} : 
        JSON.parse(localStorage.getItem("main_page_config"));

    const [compState, setCompState] = useState("loading")
    const [showModal, setShowModal] = useState(false)
   
    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    const onChooseLabel = (label, status) => 
    {
        localStorage["main_page_config"] = JSON.stringify({ notes_label: label, notes_status: status});
        setCompState("rerender");
        props.app_rerender();
    }

    const onDeleteLabel = (label) =>
    {
        setCompState("deleting_label");

        if (main_page_config.notes_label === label)
            localStorage["main_page_config"] = JSON.stringify({ notes_label: "", notes_status: "active"});

        delete_user_label(label).then( (result) =>
        {
            setCompState("loading");
        });
    }

    const onOpenModal = () => { setShowModal(true); } 
    const onCloseModal = () => { setShowModal(false); }
    const onAddLabel = () => {
        setShowModal(false);
        setCompState("loading");
        props.app_rerender(); 
    }

    // - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    if (compState === "loading")
    {
        get_user_labels().then( (result) => 
        {
            label_list = result;
            setCompState("rerender");
        });
    }
    else if (compState === "rerender")
    {
        lables = label_list.map((label) => 
            <Label 
                key={label} 
                label={label} 
                click_callback={onChooseLabel} 
                label_delete_callback={onDeleteLabel}
                choosen={label === main_page_config.notes_label} 
            /> 
        );

        setCompState("idle");
    }

    return (<>
        <AddLabelModal show={showModal} closeModal={onCloseModal} label_list={label_list} onAddLabel={onAddLabel}/>
        {
            (compState === "loading" || compState === "deleting_label") ? <>
                <Spinner animation="grow" style={{margin: "7% 50%"}} className="opacity-100"/>
                <Spinner animation="grow" style={{margin: "7% 50%"}} className="opacity-75"/>
                <Spinner animation="grow" style={{margin: "7% 50%"}} className="opacity-50"/>
                <Spinner animation="grow" style={{margin: "7% 50%"}} className="opacity-25"/>
            </>
            : <>
                <Row style={{padding: "10px 20px"}} >
                    <Button 
                        className="text-start" 
                        variant={ (main_page_config.notes_label === "" && main_page_config.notes_status === "active" ? "" : "outline-") + "secondary" }
                        onClick={ main_page_config.notes_label === "" && main_page_config.notes_status === "active" ? null : () => { onChooseLabel("", "active") }  }
                    >
                        <i className="bi bi-book-fill"></i>
                        <span> Notes</span>
                    </Button>
                </Row>

                <hr className="hr" />

                { lables }
                <Row style={{padding: "10px 20px"}} >
                    <Button 
                        className="text-start" 
                        variant="outline-info"
                        onClick={onOpenModal}
                    >
                        <i className="bi bi-plus"></i>
                        <span> Add label</span>
                    </Button>
                </Row>

                <hr className="hr" />

                <Row style={{padding: "10px 20px"}} >
                    <Button 
                        className="text-start" 
                        variant={(main_page_config.notes_label === "" && main_page_config.notes_status === "archived" ? "" : "outline-") + "success" }
                        onClick={() => { onChooseLabel("","archived"); } }
                    >
                        <i className="bi bi-archive-fill"></i>
                        <span> Archive</span>
                    </Button>
                </Row>
                <Row style={{padding: "10px 20px"}} >
                    <Button 
                        className="text-start" 
                        variant={(main_page_config.notes_label === "" && main_page_config.notes_status === "deleted" ? "" : "outline-") + "danger" }
                        onClick={() => { onChooseLabel("","deleted"); } }
                    >
                        <i className="bi bi-trash-fill"></i>
                        <span> Trash</span>
                    </Button>
                </Row>
            </>
        }
    </>)
}

export { LabelChooser }