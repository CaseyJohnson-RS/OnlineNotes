import { useState, useCallback } from 'react';

import { Row, Col } from 'react-bootstrap';

import { LabelChooser } from '../components/MainPage/LabelChooser';
import { NoteCoverBoard } from '../components/MainPage/NoteCoverBoard';


function NoteEditor(props) {
  const [, updateState] = useState();

  return (
    <>
      <Row>
        <Col xs={3}>
          <LabelChooser app_rerender={props.app_rerender}/>
        </Col>
        <Col xs={9}>
          <NoteCoverBoard />
        </Col>
      </Row>
    </>
  );
}

export { NoteEditor }