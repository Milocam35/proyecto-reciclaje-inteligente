import axios from "axios";

const API_URL = "https://rdn6x8ojtd.execute-api.us-east-1.amazonaws.com/events";

export const getEvents = async (page = 1, pageSize = 2) => {
  try {
    const response = await axios.get(API_URL, {
      params: { page, page_size: pageSize },
    });
    return response.data;
  } catch (error) {
    console.error("Error al obtener los eventos:", error);
    throw error;
  }
};
