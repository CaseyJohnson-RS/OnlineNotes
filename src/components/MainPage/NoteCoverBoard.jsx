import { useState, useCallback } from 'react';
import { NoteCover } from './NoteCover';

import { Col, Row } from 'react-bootstrap';


function NoteCoverBoard(props) {

  const [, updateState] = useState();
  const component_rerender = useCallback(() => updateState({}), []);

  /*
    title, 
    content, 
    color, 
    note_status, // active, archived, deleted
    note_id, 

    update_note_status_callback,
    open_note_callback
*/

  return (
    <>
        <Row>
        <Col xs={6}>
            <NoteCover 
              title="Header1" 
              content="Lorem ipsum и тд и тп, дада, даадааа, хаха, щекотно!..Lorem ipsum и тд и тп, дада, даадааа, хаха, щекотно!..Lorem ipsum и тд и тп, дада, даадааа, хаха, щекотно!..Lorem ipsum и тд и тп, дада, даадааа, хаха, щекотно!..Lorem ipsum и тд и тп, дада, даадааа, хаха, щекотно!..Lorem ipsum и тд и тп, дада, даадааа, хаха, щекотно!.." 
              color="#000000"
              note_id={0}
              note_status="archived"
              

            />
        </Col>
        <Col xs={6}>
            <NoteCover 
              title="Header 2" 
              content="Стена, на ней картина, в столе дырка, бежит марина, успеть бы толька..." 
              color="#555555"
              note_id={1}
              note_status="deleted"
              

            />
        </Col>
    </Row>
    </>
  );
}

export { NoteCoverBoard }