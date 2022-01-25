import { memo, VFC } from "react";

type ModalProps = {
  setModal: () => void;
};
export const ModalButton: VFC<ModalProps> = memo((props) => {
  const { setModal } = props;
  return (
    <button
      onClick={setModal}
      className="rounded-3xl bg-green-300 mt-8 w-36 h-12 stext-black hover:bg-green-500 hover:text-white"
    >
      Open
    </button>
  );
});
