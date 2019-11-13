import {
  ActionType,
  GetResourceFromServer,
  PostDataToServer
  } from "../actions/types";
  
  const initialState = {
    test2: "test2",
    test1: "test1",
    testNum: 0,
  };
  
  export default (state = initialState, action) => {
    switch (action.type) {
    case GetResourceFromServer:
      return {testNum:action.payload.num, ...state}
    case PostDataToServer:
      return state;
    default:
        return state;
    }
  };
  