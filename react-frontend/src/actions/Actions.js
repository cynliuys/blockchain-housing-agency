import {
    GetResourceFromServer,
    PostDataToServer
} from './types'
import axios from 'axios'

const yourServerUrl = "http://localhost:8080"

// Send a POST request
const postConfig = {
    method: 'post',
    url: yourServerUrl,
    data: {
        yourDataToBeSentToServer: "test"
    }
}

const getConfig = {
    method: 'get',
    url: yourServerUrl,
}

// Get resource from server
export const getResourceFromServer = () => async (dispatch, getState) => {
    // GET request for remote image
    axios(getConfig).then((res)=>{
        dispatch(modifyNumInReduxStore(res.data.num))
    }).catch((err)=>{
        console.log(`error of fetching resources is ${err}`)
    });
}

// Post data to server
export const postDataToServer = () => async (dispatch, getState) => {
    // GET request for remote image
    axios(postConfig).then((res)=>{
        console.log(`Any response from the server: ${res}`)
        dispatch({type: PostDataToServer, payload: null})
    }).catch((err)=>{
        console.log(`error of posting data is ${err}`)
    });
}

// Get image by index
export const modifyNumInReduxStore = (num) => ({
    type: GetResourceFromServer,
    payload: { num: num },
})
