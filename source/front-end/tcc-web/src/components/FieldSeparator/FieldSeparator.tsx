type Props = {
  margin?: number;
}

const FieldSeparator = ({ margin = 3 }: Props) => {
  return (
    <hr style={{ margin: `${margin}% 0` }} />
  )
}

export default FieldSeparator;