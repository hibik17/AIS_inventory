import { useState } from "react";
import { memo, VFC } from "react";
import { ModalButton } from "../atom/ModalButton";
import { BookModal } from "./BookModal";
import { ResponseType } from "../types/Response";
import { Link } from "react-router-dom";

export const NewsCard: VFC<{ response: ResponseType }> = memo(
  ({ response }) => {
    const [showModal, setShowModal] = useState(false);
    const setModal = () => {
      setShowModal(!showModal);
    };
    return (
      <div className="p-8 border border-gray-200 rounded bg-white w-96 hover:bg-gray-50 hover:border-b-4 hover:border-b-blue-500 mr-16 mb-6 animate-fade-in-down">
        <div className="flex justify-center items-center text-gray-500">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-24 w-24"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 5c7.18 0 13 5.82 13 13M6 11a7 7 0 017 7m-6 0a1 1 0 11-2 0 1 1 0 012 0z"
            />
          </svg>
        </div>
        <div className="text-center mt-4">
          <h1 className="font-bold text-gray-700 text-4xl text">
            {response.news.title}
          </h1>
          <p className="text-500 text-sm mt-4 mb-10">{response.news.summary}</p>
          <Link to={response.news.url} className="pt-16 text-blue-700 ">
            ニュースはこちら
          </Link>
          <br />
          <ModalButton setModal={setModal} />
        </div>
        {/* modalの表示 */}
        <BookModal
          showModal={showModal}
          setModal={setModal}
          response={response.book}
        />
      </div>
    );
  }
);
